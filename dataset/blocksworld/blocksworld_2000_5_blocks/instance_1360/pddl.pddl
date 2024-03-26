

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b c)
(on c e)
(on d a)
(on e d)
(clear b)
)
(:goal
(and
(on b d)
(on e b))
)
)



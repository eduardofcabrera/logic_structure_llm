

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b d)
(on c e)
(on d a)
(ontable e)
(clear b)
)
(:goal
(and
(on c e)
(on e b))
)
)





(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b d)
(on c e)
(on d c)
(on e a)
(clear b)
)
(:goal
(and
(on d e)
(on e c))
)
)





(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b a)
(on c d)
(ontable d)
(on e c)
(clear b)
)
(:goal
(and
(on a c)
(on c e))
)
)



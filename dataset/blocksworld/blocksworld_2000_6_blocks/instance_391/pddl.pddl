

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b a)
(ontable c)
(on d b)
(on e c)
(clear d)
)
(:goal
(and
(on a c)
(on c e)
(on d b))
)
)



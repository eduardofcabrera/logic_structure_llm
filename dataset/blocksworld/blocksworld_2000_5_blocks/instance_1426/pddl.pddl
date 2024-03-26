

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b e)
(ontable c)
(on d a)
(ontable e)
(clear b)
(clear d)
)
(:goal
(and
(on a e)
(on c d)
(on d a)
(on e b))
)
)


